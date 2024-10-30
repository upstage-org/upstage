from ariadne import gql


type_defs = gql("""
    type Query {
        hello: String!
    }
                
    type Mutation {
        oneTimePurchase(input: OneTimePurchaseInput!): CommonResponse
        createSubscription(input: CreateSubscriptionInput!): CommonResponse
        cancelSubscription(subscription_id: String!): CommonResponse
        updateEmailCustomer(customer_id: String!, email: String!): CommonResponse
    }

    input OneTimePurchaseInput {
        cardNumber: String!
        expYear: String!
        expMonth: String!
        cvc: String!
        amount: Float!
    }
            
    input CreateSubscriptionInput {
        cardNumber: String!
        expYear: String!
        expMonth: String!
        cvc: String!
        amount: Float!
        currency: String!
    }
                    
    type CommonResponse {
        success: Boolean
        message: String
    }
""")
