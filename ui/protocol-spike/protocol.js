client = new Paho.MQTT.Client(location.hostname, Number(1883), randomElementId());

client.onConnectionLost = onConnectionLost;
client.onMessageArrived = onMessageArrived;

client.connect({onSuccess:onConnect});


function onConnect() {
    setConnectionStatus({status: "good"});
    console.log("onConnect");
    client.subscribe("stage");
}

function onConnectionLost(responseObject) {
  if (responseObject.errorCode !== 0) {
    console.log("onConnectionLost:"+responseObject.errorMessage);
    setConnectionStatus({status: "bad"});
  }
}

function onMessageArrived(message) {
  console.log("onMessageArrived:"+message.payloadString);
  try {
    onMessageRecieved(JSON.parse(message.payloadString));
  } catch (ex) {
      console.error(`Caught: ${ex}`);
  }
}

function sendMessage(msg) {
    if (typeof msg.details.target == "object") {
        msg.details.target = msg.details.target.id;
    }
    console.log(`Sending message to broker: ${msg}`);
    const message = new Paho.MQTT.Message(JSON.stringify(msg));
    message.destinationName = "stage";
    client.send(message);
}

async function onMessageRecieved(msg) {
    console.log(`Message recieved from broker: ${msg}`);
    const action = window[msg.type];
    if (typeof action == "function") {
        if (msg.details.target) {
            const target = document.getElementById(msg.details.target);
            if (target == undefined) {
                console.error(`Invalid message: ${msg}`);
            } else {
                msg.details.target = target;
            }
        }
        action(msg.details);
    }
}