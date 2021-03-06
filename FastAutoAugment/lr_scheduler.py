import torch

from theconf import Config as C


def adjust_learning_rate_pyramid(optimizer, max_epoch):
    def __adjust_learning_rate_pyramid(epoch):
        """Sets the learning rate to the initial LR decayed by 10 every 30 epochs"""
        base_lr = C.get()['lr']
        if C.get()['gradual']['lr'] > 1:
            base_lr *= C.get()['gradual']['lr'] * min(1.0, epoch / C.get()['gradual']['epoch'])
        lr = base_lr * (0.1 ** (epoch // (max_epoch * 0.5))) * (0.1 ** (epoch // (max_epoch * 0.75)))

        for param_group in optimizer.param_groups:
            param_group['lr'] = lr

    return torch.optim.lr_scheduler.LambdaLR(optimizer, __adjust_learning_rate_pyramid)


def adjust_learning_rate_resnet(optimizer):
    """
    Sets the learning rate to the initial LR decayed by 10 every [90, 180, 240] epochs
    Ref: AutoAugment
    """

    if C.get()['epoch'] == 90:
        return torch.optim.lr_scheduler.MultiStepLR(optimizer, [30, 60, 80])
    elif C.get()['epoch'] == 270:   # autoaugment
        return torch.optim.lr_scheduler.MultiStepLR(optimizer, [90, 180, 240])
    else:
        raise ValueError('invalid epoch=%d for resnet scheduler' % C.get()['epoch'])
