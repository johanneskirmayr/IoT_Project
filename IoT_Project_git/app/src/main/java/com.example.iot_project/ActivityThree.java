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

public class ActivityThree extends AppCompatActivity {

    TextView info_field, room_field;
    Button reset_button;
    String room_topic, command_topic;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_three);

        info_field = (TextView) findViewById(R.id.info_field_activity_three);
        room_field = (TextView) findViewById(R.id.info_field_last_beacon);
        reset_button = (Button) findViewById(R.id.third_activity_reset_button);

        info_field.setText("Insert picture here");
        room_field.setText("Last passed Beacon: NaN");

        room_topic = "iotlab/jj/rooms";
        command_topic = "iotlab/jj/commands";

        reset_button.setOnClickListener(v -> {
            publish(command_topic, "RESET");
            disconnect();
            Intent intent = new Intent(ActivityThree.this, MainActivity.class);
            startActivity(intent);
        });

        connect();

        client.setCallback(new MqttCallbackExtended() {
            @Override
            public void connectComplete(boolean reconnect, String serverURI) {
                if (reconnect) {
                    System.out.println("Reconnected to : " + serverURI);
                    subscribe(room_topic);
                    subscribe(command_topic);
                } else {
                    System.out.println("Connected to: " + serverURI);
                    subscribe(room_topic);
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
                System.out.println("Activity3 Incoming message: " + newMessage);

                if (topic.equals(room_topic)) {
                    room_field.setText("Last passed beacon: " + newMessage);
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
        final String topic = topicToPublish;
        final String message = messageToPublish;
        try {
            client.publish(topic, message.getBytes(),0,false);
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
                    System.out.println("Activity3 disconnected!");
                }

                @Override
                public void onFailure(IMqttToken asyncActionToken, Throwable exception) {
                    System.out.println("Activity3 could not disconnect!");
                }
            });
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }
}
