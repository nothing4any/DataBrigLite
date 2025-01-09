import { defineStore } from 'pinia';

export const useTitleStore = defineStore('title', {
    state: () => ({
        title: '默认标题'
    }),
    actions: {
        setTitle(newTitle) {
            this.title = newTitle;
            document.title = newTitle;
        }
    }
});
