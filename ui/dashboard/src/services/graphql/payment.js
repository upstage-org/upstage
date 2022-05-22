import { gql } from "graphql-request";
import { createClient } from "./graphql";

const client = createClient('payment_graphql')

export default {
    oneTimePurchase: (input) => client.request(gql`
    mutation{
        oneTimePurchase(
            input: {
                cardNumber: "${input.cardNumber}",
                expYear: 20${input.expYear},
                expMonth: ${input.expMonth},
                cvc: ${input.cvc},
                amount:${input.amount}
            })
        {      
            success 
        }
    }`),
}