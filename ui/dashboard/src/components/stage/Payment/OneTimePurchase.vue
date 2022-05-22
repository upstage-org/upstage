<template>
  <div class="payment">
    <div id="amounts">
      <h4>Pay What You Can:</h4>
      <div id="choice-buttons">
        <div>
          <span class="input-symbol-dollar"></span>
          <button class="button  payment-button" @click="amount = 10"><span>10</span></button>
        </div>
        <div>
          <span class="input-symbol-dollar"></span>
          <button class="button  payment-button" @click="amount = 20"><span>20</span></button>
        </div>
        <div>
          <span class="input-symbol-dollar"></span>
          <button class="button  payment-button" @click="amount = 30"><span>30</span></button>
        </div>
        <div>
          <span class="input-symbol-dollar"></span>
          <input 
            ref="custom_amount" 
            type="number" 
            step="0.01" min="0" max="999999.99" 
            class="button payment-button"
            placeholder="Custom" 
            @input="amount = $event.target.value" 
            :value="amount == 0 ? 'Custom' : amount"
          >
        </div>
      </div>
      <div class="column">
        <button id="purchase" class="button is-primary" @click="openPurchasePopup()">
          <span>Donate to Upstage</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "@vue/reactivity";
import { useStore } from "vuex";
import { notification } from "@/utils/notification";

export default {
  setup: () => {
    const store = useStore();
    const amount = ref(0);

    const openPurchasePopup = () => {
      if (amount.value != 0) {
        store
          .dispatch("stage/openPurchasePopup", {
            type: 'OneTimePurchase',
            amount: amount.value,
            title: 'Donate to Upstage'
          });
        amount.value = 0
      } else {
        notification.warning('Please select amount to donate!');
      }
    }

    return { amount, openPurchasePopup }
  }
}
</script>
<style  lang="scss" scoped>
#amounts {
  margin-left: 20%;
  width: 60%;
  display: grid;
  grid-template-columns: 1fr 2fr 1fr;

  h4 {
    font-size: 1.25em;
    font-weight: 400;
    margin-top: 16px;
  }
}

#choice-buttons {
  margin-top: 3%;
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 3fr;

  .button {
    position: inherit;
  }

  .payment-button {
    width: calc(100% - 10px);
    font-family: inherit;
  }

  .input-symbol-dollar {
    position: relative;
    display: block;
  }

  .input-symbol-dollar::before {
    content: "$";
    position: absolute;
    display: block;
    height: 100%;
    top: 0;
    left: 10px;
    line-height: 40px;
  }
}
</style>