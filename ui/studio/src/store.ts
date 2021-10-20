import { InjectionKey } from 'vue'
import { createStore, Store, useStore } from 'vuex'
import studioGraph from './services/graphql/studio'

// define your typings for the store state
export interface State {
  count: number
}

// define injection key

export const store = createStore<State>({
  state: {
    count: 0
  },
  mutations: {
    INCREASE(state) {
      state.count += 1
    }
  },
  actions: {
    init({ dispatch }) {
      dispatch('fetchMedia')
    },
    async fetchMedia() {
      const res = await studioGraph.mediaList()
      console.log(res)
    }
  }
})

export const key: InjectionKey<Store<State>> = Symbol()

export const useStudioStore = () => useStore(key)