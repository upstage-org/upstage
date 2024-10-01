from ariadne import gql

type_defs = gql("""
    type Mutation {
        sendEmailExternal(emailInfo: EmailInput!): EmailResponse!
    }
                
    type Query {
        _: Boolean
    }

    input EmailInput {
        subject: String!
        body: String!
        recipients: [String!]
        cc: [String!]
        bcc: [String!]
        filenames: [String!]
    }

    type EmailResponse {
        success: Boolean!
    }
""")
