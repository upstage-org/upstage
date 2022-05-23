<template>
  <transition name="fade">
    <div class="modal" :class="{ 'is-active': isActive }">
      <div class="modal-background" @click="close"></div>
      <div class="modal-content">
        <div class="card">
          <a href="#" class="card-header-icon" @click="close">
            <span class="icon">
              <Icon src="close.svg" />
            </span>
          </a>
          <div class="card-header">
            <span class="card-header-title">{{ title }}</span>
          </div>
          <div class="card-content">
            <!-- <div class="input block-input">
              <span class="icon card-icon">
                <i class="fas fa-envelope"></i>
              </span>
              <input class="card-input input" type="email" x-autocompletetype="email" autocompletetype="email"
                placeholder="Email" v-model="card.email" required>
            </div> -->
            <div class="block-input">
              <div class="input">
                <span class="icon card-icon">
                  <i class="fas fa-credit-card"></i>
                </span>
                <input
                  required
                  class="card-input input"
                  type="tel"
                  placeholder="Card Number"
                  v-model="card.cardNumber"
                  onkeypress="return /[0-9]/i.test(event.key)"
                />
              </div>
              <div class="card-secret-info">
                <div class="input">
                  <span class="icon card-icon">
                    <i class="fas fa-calendar"></i>
                  </span>
                  <input
                    required
                    v-model="card.exp"
                    onkeypress="return /[0-9]/i.test(event.key)"
                    maxlength="5"
                    class="card-input input"
                    type="tel"
                    placeholder="MM/YY"
                    @input="
                      $event.target.value = formatExp($event.target.value)
                    "
                    @keydown.delete="
                      $event.target.value = deleteKeyDownExp(
                        $event.target.value
                      )
                    "
                  />
                </div>
                <div class="input">
                  <span class="icon card-icon">
                    <i class="fas fa-lock"></i>
                  </span>
                  <input
                    required
                    class="card-input input"
                    type="tel"
                    placeholder="CVC"
                    onkeypress="return /[0-9]/i.test(event.key)"
                    maxlength="3"
                    v-model="card.cvc"
                  />
                </div>
              </div>
            </div>
            <div class="button-purchase">
              <button
                class="button is-primary"
                @click="donateToUpstage()"
                :class="{
                  'is-loading': loading,
                }"
                :disabled="loading"
              >
                <span>Donate $ {{ amount }}</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
import { computed, ref } from "vue";
import { useStore } from "vuex";
import Icon from "@/components/Icon";
import { paymentGraph } from "@/services/graphql";
import { useMutation } from "@/services/graphql/composable";
import { notification } from "@/utils/notification";

export default {
  components: { Icon },
  setup: () => {
    const store = useStore();
    console.log(store.state.stage.purchasePopup);
    const isActive = computed(() => store.state.stage.purchasePopup.isActive);
    const title = computed(() => store.state.stage.purchasePopup.title);
    const amount = computed(() => store.state.stage.purchasePopup.amount);
    const modal = ref();
    const loading = ref(false);
    const card = ref({
      email: "",
      cardNumber: "",
      exp: "",
      cvc: "",
    });

    const close = () => {
      store.dispatch("stage/closePurchasePopup");
    };

    const formatExp = (value) => {
      if (value.length == 3 && !value.includes("/")) {
        value = `${value.substring(0, 2)}/${value.slice(-1)}`;
      }
      return value;
    };
    const deleteKeyDownExp = (value) => {
      if (value.length == 4 && value[2] == "/") {
        value = value.slice(0, -1);
      }
      return value;
    };

    return {
      isActive,
      close,
      modal,
      title,
      amount,
      card,
      paymentGraph,
      loading,
      formatExp,
      deleteKeyDownExp,
    };
  },
  methods: {
    async donateToUpstage() {
      try {
        this.loading = true;
        if (!this.card.cardNumber || !this.card.exp || !this.card.cvc) {
          notification.warning("Please input card information!");
          return;
        }
        if (
          this.card.length < 5 ||
          !/[0-9]{2}\/[0-9]{2}/i.test(this.card.exp)
        ) {
          notification.warning("Please input exp card (MM/YY)!");
          return;
        }
        if (this.card.cvc.length < 3) {
          notification.warning("Please input 3 cvc numbers!");
          return;
        }
        const { mutation } = useMutation(paymentGraph.oneTimePurchase, {
          cardNumber: this.card.cardNumber,
          expYear: this.card.exp.slice(-2),
          expMonth: this.card.exp.substring(0, 2),
          cvc: this.card.cvc,
          amount: this.amount,
        });
        await mutation().then((res) => {
          if (res.oneTimePurchase.success) {
            notification.success("Donate to Upstage success!");
          } else {
            notification.error("Donate to Upstage failure!");
          }
          this.loading = false;
          this.close();
        });
      } catch (error) {
        notification.error(error);
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>
<style scoped lang="scss">
.card-icon {
  position: absolute;
  display: block;
  height: 100%;
  line-height: 40px;
}

.card-input {
  position: inherit;
  display: block;
  margin-left: 1.5rem;
  border: none;
  background-color: transparent;
  width: calc(100% - 1.5rem);
  font-family: inherit;
}

.card-input:focus {
  border-color: inherit;
  -webkit-box-shadow: none;
  box-shadow: none;
}

.block-input {
  margin-bottom: 18px;
}

.card-secret-info {
  display: grid;
  grid-template-columns: 1fr 1fr;
}

.button-purchase {
  display: grid;
  grid-template-columns: 1fr;
}

.card-header-icon {
  position: absolute;
  right: 0;
}
</style>