#include <linux/module.h>
#include <linux/moduleparam.h>
#include <linux/kernel.h>
#include <linux/init.h>

#include <linux/interrupt.h>
#include <linux/gpio.h>

#include <linux/netlink.h>
#include <net/netlink.h>
#include <net/net_namespace.h>

#define irq_to_gpio(x)              ((x) - gpio_to_irq(0))

#define GPIO_ANY_GPIO_DESC          "some gpio pin description"
#define GPIO_ANY_GPIO_DEVICE_DESC   "some_device"
#define MY_PROTO                    NETLINK_USERSOCK
#define MY_GROUP                    31

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Andreas Stefl");
MODULE_DESCRIPTION("time vs time client");

static int pin = 0;
static int pid = -1;
static short int irq = 0;
static struct sock* nlsock = NULL;

module_param(pin, int, S_IRUSR | S_IWUSR | S_IRGRP | S_IROTH);
MODULE_PARM_DESC(pin, "gpio pin");
module_param(pid, int, S_IRUSR | S_IWUSR | S_IRGRP | S_IROTH);
MODULE_PARM_DESC(pid, "pid");

static void nlsock_send(void* msg, unsigned int size);

static irqreturn_t irq_handler(int irq, void *dev_id, struct pt_regs *regs) {
    unsigned long flags;
    
    // disable hard interrupts (remember them in 'flags')
    local_irq_save(flags);
    
    // restore hard interrupts
    local_irq_restore(flags);
    
    nlsock_send("interrupt", 9);
    printk(KERN_NOTICE "interrupt [%d]\n", irq_to_gpio(irq), (char *) dev_id);
    
    return IRQ_HANDLED;
}

static void int_config(void) {
    if (gpio_request(pin, GPIO_ANY_GPIO_DESC)) {
        printk("GPIO request faiure: %s\n", GPIO_ANY_GPIO_DESC);
        return;
    }
    
    irq = gpio_to_irq(pin)
    if (irq < 0) {
        printk("GPIO to IRQ mapping faiure %s\n", GPIO_ANY_GPIO_DESC);
        return;
    }
    
    printk(KERN_NOTICE "Mapped int %d\n", irq);
    
    if (request_irq(irq, (irq_handler_t) irq_handler,
                         IRQF_TRIGGER_FALLING,
                         GPIO_ANY_GPIO_DESC,
                         GPIO_ANY_GPIO_DEVICE_DESC)) {
        printk("Irq failure\n");
        return;
    }
}

static void int_release(void) {
    free_irq(irq, GPIO_ANY_GPIO_DEVICE_DESC);
    gpio_free(pin);
}

static void nlsock_send(void* msg, unsigned int size) {
    struct sk_buff* skb_out;
    struct nlmsghdr* nlh;
    int res;
    
    skb_out = nlmsg_new(size, GFP_KERNEL);
    if (skb_out == NULL) {
        printk(KERN_ERR "Failed to allocate new skb\n");
        return;
    }
    
    nlh = nlmsg_put(skb_out, 0, 0, NLMSG_DONE, size, 0);
    strncpy(nlmsg_data(nlh), msg, size);
    
    if (pid == -1) {
        res = nlmsg_multicast(nlsock, skb_out, 0, MY_GROUP, GFP_KERNEL);
    } else {
        res = nlmsg_unicast(nlsock, skb_out, pid);
    }
    if (res < 0) {
        printk(KERN_INFO "Error while sending to user\n");
        return;
    }
}

static void nlsock_config(void) {
    nlsock = netlink_kernel_create(&init_net, MY_PROTO, NULL);
    if (nlsock == NULL) {
        pr_err("Error creating netlink.\n");
        return;
    }
}

static void nlsock_release(void) {
    netlink_kernel_release(nlsock);
}

static int init(void) {
    printk(KERN_NOTICE "Hello\n");
    
    nlsock_config();
    int_config();
    
    return 0;
}

static void cleanup(void) {
    printk(KERN_NOTICE "Goodbye\n");
    
    int_release();
    nlsock_release();
}


module_init(init);
module_exit(cleanup);

