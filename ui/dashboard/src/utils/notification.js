import { toast as bulmaToast } from "bulma-toast";
import anime from "animejs";

export const toast = props => {
    bulmaToast({
        type: 'is-primary',
        dismissible: true,
        closeOnClick: false,
        duration: 10000,
        offsetTop: '50px',
        offsetRight: '-50px',
        ...props,
    });

    anime({
        targets: '.notification',
        translateX: '-50px',
    });
}

export const notification = {
    success: message => {
        toast({ message, type: 'is-success' })
    },
    info: message => {
        toast({ message, type: 'is-info' })
    },
    warning: message => {
        toast({ message, type: 'is-warning' })
    },
    error: message => {
        toast({ message, type: 'is-danger' })
    },
}