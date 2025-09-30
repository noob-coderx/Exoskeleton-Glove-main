using UnityEngine;
using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Collections.Generic;
using System.Security.Claims;
using Unity.VisualScripting;

public class HandController : MonoBehaviour
{
    // Finger joint transforms
    public Transform middle1;
    public Transform middle2;
    public Transform middle3;
    public Transform index3;
    public Transform index1;
    public Transform index2;
    public Transform ring3;
    public Transform ring1;
    public Transform ring2;
    public Transform little3;
    public Transform little1;
    public Transform little2;
    public Transform thumb2;
    public Transform thumb1;

    // UDP communication members
    private UdpClient udpClient;
    private Thread receiveThread;
    private volatile bool running = true;

    // Calibration and timing state
    private bool calibrationStarted = false;
    private bool calibrationComplete = false;
    private const int jointCount = 12;
    private List<float>[] calibrationValues = new List<float>[jointCount];
    private bool[] jointCalibrated = new bool[jointCount];
    private bool[] jointInvalid = new bool[jointCount];
    private float countdownTimer = 10f;
    private bool ackPartialCalibration = false;

    // Default angle values
    public float index3_default;
    public float index2_default;
    public float index1_default;
    public float middle3_default;
    public float middle2_default;
    public float middle1_default;
    public float ring3_default;
    public float ring2_default;
    public float ring1_default;
    public float little3_default;
    public float little2_default;
    public float little1_default;
    public float thumb2_default;
    public float thumb1_default;

    // Live angle data
    private float[] latestAngles = new float[jointCount];
    private bool[] hasNewData = new bool[jointCount];

    void Start()
    {
        for (int i = 0; i < jointCount; i++)
        {
            calibrationValues[i] = new List<float>();
            jointCalibrated[i] = false;
            jointInvalid[i] = false;
        }

        udpClient = new UdpClient(12345);
        receiveThread = new Thread(ReceiveData);
        receiveThread.IsBackground = true;
        receiveThread.Start();
        Debug.Log("UDP Listener started. Press Start to begin calibration.");
    }

    void OnGUI()
    {
        if (!calibrationStarted)
        {
            if (GUI.Button(new Rect(Screen.width / 2 - 75, Screen.height / 2 - 25, 150, 50), "Start Calibration"))
            {
                calibrationStarted = true;
                countdownTimer = 10f;
                ackPartialCalibration = false;
                Debug.Log("Calibration started with 10 second timeout");
            }
        }
        else if (!calibrationComplete)
        {
            // Countdown display
            GUI.Label(new Rect(Screen.width / 2 - 100, Screen.height / 2 - 100, 200, 50),
                    $"Hold your hand still!! \n Time Remaining: {Mathf.CeilToInt(countdownTimer)}",
                    new GUIStyle { fontSize = 20, alignment = TextAnchor.MiddleCenter });

            // Calibration status
            GUI.Label(new Rect(Screen.width / 2 - 100, Screen.height / 2 - 50, 200, 50),
                    "Calibrating...",
                    new GUIStyle { fontSize = 20, alignment = TextAnchor.MiddleCenter });
        }
        else
        {
            bool anyInvalid = false;
            foreach (bool invalid in jointInvalid) if (invalid) anyInvalid = true;

            if (anyInvalid && !ackPartialCalibration)
            {
                // Partial calibration warning
                GUI.color = Color.yellow;
                GUI.Label(new Rect(Screen.width / 2 - 200, Screen.height / 2 - 50, 400, 100),
                        "<size=24>Partial Calibration!</size>\n<size=18>Some joints disabled</size>",
                        new GUIStyle
                        {
                            alignment = TextAnchor.MiddleCenter,
                            richText = true
                        });

                if (GUI.Button(new Rect(Screen.width / 2 - 50, Screen.height / 2 + 60, 100, 30), "OK"))
                {
                    ackPartialCalibration = true;
                }
            }
            else
            {
                // Final status display
                string statusMessage = "Calibration Complete!";
                Color statusColor = anyInvalid ? Color.yellow : Color.green;

                GUI.color = statusColor;
                GUI.Label(new Rect(Screen.width / 4 - 30, Screen.height / 3, 300, 50),
                        statusMessage,
                        new GUIStyle
                        {
                            fontSize = 24,
                            alignment = TextAnchor.MiddleCenter,
                            richText = true
                        });
            }
        }
    }

    void Update()
    {
        // Handle calibration timeout
        if (calibrationStarted && !calibrationComplete)
        {
            countdownTimer -= Time.deltaTime;

            if (countdownTimer <= 0f)
            {
                calibrationComplete = true;
                Debug.Log("Calibration timeout reached!");

                // Mark joints with no data as invalid
                for (int i = 0; i < jointCount; i++)
                {
                    if (calibrationValues[i].Count == 0)
                    {
                        jointInvalid[i] = true;
                        Debug.Log($"Joint {i} disabled - no calibration data");
                    }
                    else
                    {
                        Debug.Log($"Joint {i} enabled - calibration data received");
                    }
                }
            }
        }

        // Apply rotations for valid joints
        if (calibrationComplete)
        {
            for (int bit = 0; bit < jointCount; bit++)
            {
                if (hasNewData[bit] && !jointInvalid[bit])
                {
                    hasNewData[bit] = false;
                    ApplyRotation(bit, latestAngles[bit]);
                }
            }
        }
    }

    void ApplyRotation(int jointIndex, float angle)
    {
        switch (jointIndex)
        {

            case 0: index3.localRotation = Quaternion.Euler(0, 0, 2 * angle);break;// Debug.Log("index top: "+angle); break;
            case 1: index2.localRotation = Quaternion.Euler(0, 0, 2 * angle); break;// Debug.Log("index mid: " + angle); break;
            case 2: index1.localRotation = Quaternion.Euler(0, 0, 3 * angle); break;//Debug.Log("index bot: " + angle); break;
            case 3: middle3.localRotation = Quaternion.Euler(0, 0, 3 * angle); break;//Debug.Log("middle top: " + angle); break;
            case 4: middle2.localRotation = Quaternion.Euler(0, 0, 4 * angle); break;
            case 5: middle1.localRotation = Quaternion.Euler(0, 0, angle); break;//Debug.Log("middle bot: " + angle); break;
            case 6: ring3.localRotation = Quaternion.Euler(0, 0, 9 * angle); break;//Debug.Log("ring top: " + angle); break;
            case 7: ring2.localRotation = Quaternion.Euler(0, 0, 2.5f * angle); break;//Debug.Log("ring mid: " + angle); break;
            case 8: ring1.localRotation = Quaternion.Euler(0, 0, angle); break;//Debug.Log("ring bot: " + angle); break;
            case 9: little3.localRotation = Quaternion.Euler(0, 0, angle); break;//Debug.Log("little top: " + angle); break;
            case 10: little1.localRotation = Quaternion.Euler(0, 0, 3*angle); break;//Debug.Log("little base: " + angle); break;
            case 11:thumb1.localRotation = Quaternion.Euler(0, 0, -1 * angle); break; Debug.Log("little base: " + angle); break;

        }
    }
    

    void ReceiveData()
    {
        IPEndPoint remoteEP = new IPEndPoint(IPAddress.Any, 12345);

        while (running)
        {
            try
            {
                byte[] data = udpClient.Receive(ref remoteEP);
                string message = Encoding.UTF8.GetString(data);
                string[] parts = message.Split(' ');

                if (parts.Length < 2 ||
                    !int.TryParse(parts[0], out int bit) ||
                    !float.TryParse(parts[1], out float rawAngle)) continue;

                float angle = rawAngle * 360f / 65536f;

                if (calibrationStarted && !calibrationComplete)
                {
                    if (!jointCalibrated[bit] && calibrationValues[bit].Count < 5)
                    {
                        calibrationValues[bit].Add(angle);
                        Debug.Log(bit + " " + angle);
                        if (calibrationValues[bit].Count == 5)
                        {
                            float avg = CalculateAverage(calibrationValues[bit]);
                            SetDefaultForJoint(bit, avg);
                            jointCalibrated[bit] = true;
                            CheckFullCalibration();
                        }
                    }
                }
                else if (calibrationComplete)
                {
                    latestAngles[bit] = angle - GetDefaultForJoint(bit);
                    hasNewData[bit] = true;
                }
            }
            catch (Exception e)
            {
                Debug.LogError($"UDP Error: {e.Message}");
            }
        }
    }

    float CalculateAverage(List<float> values)
    {
        float sum = 0f;
        foreach (float val in values) sum += val;
        return sum / values.Count;
    }

    void CheckFullCalibration()
    {
        for (int i = 0; i < jointCount; i++)
        {
            if (!jointCalibrated[i]) return;
        }
        calibrationComplete = true;
        Debug.Log("Full calibration achieved!");
    }

    void SetDefaultForJoint(int bit, float avg)
    {
        switch (bit)
        {
            case 0: index3_default = avg; break;
            case 1: index2_default = avg; break;
            case 2: index1_default = avg; break;
            case 3: middle3_default = avg; break;
            case 4: middle2_default = avg; break;
            case 5: middle1_default = avg; break;
            case 6: ring3_default = avg; break;
            case 7: ring2_default = avg; break;
            case 8: ring1_default = avg; break;
            case 9: little3_default = avg; break;
            case 10: little2_default = avg; break;
            case 11: little1_default = avg; break;
            case 12: thumb2_default = avg; break;
            case 13: thumb1_default = avg; break;
        }
    }

    float GetDefaultForJoint(int bit)
    {
        switch (bit)
        {
            case 0: return index3_default;
            case 1: return index2_default;
            case 2: return index1_default;
            case 3: return middle3_default;
            case 4: return middle2_default;
            case 5: return middle1_default;
            case 6: return ring3_default;
            case 7: return ring2_default;
            case 8: return ring1_default;
            case 9: return little3_default;
            case 10: return little2_default;
            case 11: return little1_default;
            case 12: return thumb2_default;
            case 13: return thumb1_default;
            default: return 0f;
        }
    }

    void OnApplicationQuit()
    {
        running = false;
        udpClient?.Close();
    }
}
