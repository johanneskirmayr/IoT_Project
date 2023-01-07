package com.example.iot_project;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.widget.Button;
import android.widget.EditText;
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

public class MainActivity extends AppCompatActivity {

    TextView info_field;
    Button call_drone_button;
    EditText room_input;
    String room_called, room_topic, command_topic;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_one);

        call_drone_button = (Button) findViewById(R.id.call_drone_button);
        info_field = (TextView) findViewById(R.id.info_field_activity_one);
        room_input = (EditText) findViewById(R.id.room_input);

        room_topic = "iotlab/jj/rooms";
        command_topic = "iotlab/jj/commands";

        info_field.setText("Hello, \n Do you need help navigating the rooms? \n Please type in where you want to go!");

        /* When the user puts in a room, publishes the room and a start command.
            Switches intent to the new activity */
        call_drone_button.setOnClickListener(v -> {
            if (room_input.getText() != null) {
                // check if room is legal
                room_called = room_input.getText().toString();
                publish(room_topic, room_called);
                publish(command_topic, "START");
                disconnect();
                Intent intent = new Intent(MainActivity.this, ActivityTwo.class);
                startActivity(intent);
            }
        });

        connect();
        // regular MQTT functions
        client.setCallback(new MqttCallbackExtended() {
            @Override
            public void connectComplete(boolean reconnect, String serverURI) {
                if (reconnect) {
                    System.out.println("Reconnected to : " + serverURI);
                    subscribe(room_topic);
                } else {
                    System.out.println("Connected to: " + serverURI);
                    subscribe(room_topic);
                }
            }

            @Override
            public void connectionLost(Throwable cause) {
                System.out.println("The Connection was lost.");
            }

            @Override
            public void messageArrived(String topic, MqttMessage message) {
                String newMessage = new String(message.getPayload());
                System.out.println("Activity1 Incoming message: " + newMessage);
            }

            @Override
            public void deliveryComplete(IMqttDeliveryToken token) {
            }
        });
    }

    private MqttAndroidClient client;
    private static final String SERVER_URI = "tcp://broker.hivemq.com:1883";
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
            client.publish(topicToPublish, messageToPublish.getBytes(), 0, false);
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
                    System.out.println("Activity1 disconnected!");
                }

                @Override
                public void onFailure(IMqttToken asyncActionToken, Throwable exception) {
                    System.out.println("Activity1 could not disconnect!");
                }
            });
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }
}
