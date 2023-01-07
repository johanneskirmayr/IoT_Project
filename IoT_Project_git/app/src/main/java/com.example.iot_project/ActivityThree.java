package com.example.iot_project;

import android.content.Intent;
import android.graphics.drawable.Drawable;
import android.media.Image;
import android.os.Bundle;
import android.util.Log;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.ContextCompat;

import com.example.iot_project.R.drawable;

import org.eclipse.paho.android.service.MqttAndroidClient;
import org.eclipse.paho.client.mqttv3.IMqttActionListener;
import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.IMqttToken;
import org.eclipse.paho.client.mqttv3.MqttCallbackExtended;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;

public class ActivityThree extends AppCompatActivity {

    TextView room_field;
    Button reset_button;
    String room_topic, command_topic;
    ImageView beacon_image;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_three);

        room_field = (TextView) findViewById(R.id.info_field_last_beacon);
        reset_button = (Button) findViewById(R.id.third_activity_reset_button);
        beacon_image = (ImageView) findViewById(R.id.beacon_image);

        room_field.setText("Last passed Beacon: null");

        room_topic = "iotlab/jj/rooms";
        command_topic = "iotlab/jj/commands";

        /* The user can reset the tour e.g. if the user wants to go to a different room.
        When this happens the activity disconnects from the browser and restarts the first activity */
        reset_button.setOnClickListener(v -> {
            publish(command_topic, "RESET");
            disconnect();
            Intent intent = new Intent(ActivityThree.this, MainActivity.class);
            startActivity(intent);
        });

        connect();
        // regular MQTT functions
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
            public void messageArrived(String topic, MqttMessage message) {
                String newMessage = new String(message.getPayload());
                System.out.println("Activity3 Incoming message: " + newMessage);

                /* If the Raspberry Pi detects a BT beacon it sends the Room.
                The activity updates the map accordingly to the room, last passed. */
                if (topic.equals(room_topic)) {
                    room_field.setText("Last passed beacon: " + newMessage);
                    System.out.println(newMessage);
                    switch (newMessage) {
                        case "A":
                            beacon_image.setImageResource(drawable.mapa);
                            break;
                        case "B":
                            beacon_image.setImageResource(drawable.mapb);
                            break;
                        case "C":
                            beacon_image.setImageResource(drawable.mapc);
                            break;
                        case "D":
                            beacon_image.setImageResource(drawable.mapd);
                            break;
                        case "E":
                            beacon_image.setImageResource(drawable.mape);
                            break;
                        case "F":
                            beacon_image.setImageResource(drawable.mapf);
                            break;
                        default: // if the room is not recognized, go to the default case
                            beacon_image.setImageResource(drawable.map);
                            room_field.setText("Last passed beacon: null");
                            break;
                    }

                } else if (topic.equals(command_topic)) {
                    /* When the raspberry Pi detects the final beacon it sends a reset.
                    This sets the application back to the start activity (MainActivity) */
                    if (newMessage.equals("RESET")) {
                        disconnect();
                        Intent intent = new Intent(ActivityThree.this, MainActivity.class);
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
    private static final String SERVER_URI = "tcp://broker.hivemq.com:1883";
    private static final String TAG = "ActivityThree";

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
