package com.example.iot_project;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.widget.Button;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;

import org.eclipse.paho.android.service.MqttAndroidClient;
import org.eclipse.paho.client.mqttv3.IMqttActionListener;
import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.IMqttToken;
import org.eclipse.paho.client.mqttv3.MqttCallbackExtended;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;

public class ActivityTwo extends AppCompatActivity {

    TextView info_field1, info_field2;
    Button reset_button;
    String command_topic;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_two);


        info_field1 = (TextView) findViewById(R.id.info_field_activity_two);
        info_field2 = (TextView) findViewById(R.id.info_field_activity_two_2);
        reset_button = (Button) findViewById(R.id.second_activity_reset_button);

        info_field1.setText("The Drone is on it's way to you!");
        info_field2.setText("The Drone will start guiding you, \n once it arrives!");

        command_topic = "iotlab/jj/commands";

        reset_button.setOnClickListener(v -> {
            publish(command_topic, "RESET");
            disconnect();
            Intent intent = new Intent(ActivityTwo.this, MainActivity.class);
            startActivity(intent);
        });

        connect();

        client.setCallback(new MqttCallbackExtended() {
            @Override
            public void connectComplete(boolean reconnect, String serverURI) {
                if (reconnect) {
                    System.out.println("Reconnected to : " + serverURI);
                    subscribe(command_topic);
                } else {
                    System.out.println("Connected to: " + serverURI);
                    subscribe(command_topic);
                }
            }
            @Override
            public void connectionLost(Throwable cause) {
                System.out.println("The Connection was lost.");
            }

            @Override
            public void messageArrived(String topic, MqttMessage message) throws
                    Exception {
                String newMessage = new String(message.getPayload());
                System.out.println("Activity2 Incoming message: " + newMessage);

               if (topic.equals(command_topic)) {
                   if (newMessage.equals("START")) {
                       disconnect();
                       Intent intent = new Intent(ActivityTwo.this, ActivityThree.class);
                       startActivity(intent);
                   }
               }

            }
            @Override
            public void deliveryComplete(IMqttDeliveryToken token) {
            }
        });
    }

    private MqttAndroidClient client;
    private static final String SERVER_URI = "tcp://test.mosquitto.org:1883";
    private static final String TAG = "MainActivity";

    private void connect() {
        String clientId = MqttClient.generateClientId();
        client =
                new MqttAndroidClient(this.getApplicationContext(), SERVER_URI,
                        clientId);
        try {
            IMqttToken token = client.connect();
            token.setActionCallback(new IMqttActionListener() {
                @Override
                public void onSuccess(IMqttToken asyncActionToken) {
                    // We are connected
                    Log.d(TAG, "onSuccess");
                    System.out.println(TAG + " Success. Connected to " + SERVER_URI);
                }

                @Override
                public void onFailure(IMqttToken asyncActionToken, Throwable exception) {
                    // Something went wrong e.g. connection timeout or firewall problems
                    Log.d(TAG, "onFailure");
                    System.out.println(TAG + " Oh no! Failed to connect to " +
                            SERVER_URI);
                }
            });
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    private void subscribe(String topicToSubscribe) {
        final String topic = topicToSubscribe;
        int qos = 1;
        try {
            IMqttToken subToken = client.subscribe(topic, qos);
            subToken.setActionCallback(new IMqttActionListener() {
                @Override
                public void onSuccess(IMqttToken asyncActionToken) {
                    System.out.println("Subscription successful to topic: " + topic);
                }
                @Override
                public void onFailure(IMqttToken asyncActionToken,
                                      Throwable exception) {
                    System.out.println("Failed to subscribe to topic: " + topic);
                }
            });
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    private void publish(String topicToPublish, String messageToPublish) {
        try {
            client.publish(topicToPublish, messageToPublish.getBytes(),0,false);
        } catch (MqttException e) {
            System.out.println(e);
        }
    }

    private void disconnect() {

        try {
            IMqttToken token = client.disconnect();
            token.setActionCallback(new IMqttActionListener() {
                @Override
                public void onSuccess(IMqttToken asyncActionToken) {
                    System.out.println("Activity2 disconnected!");
                }

                @Override
                public void onFailure(IMqttToken asyncActionToken, Throwable exception) {
                    System.out.println("Activity2 could not disconnect!");
                }
            });
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }
}