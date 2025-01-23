using BepInEx;
using UnityEngine;

[BepInPlugin("com.example.helloworldexample", "Example Plugin", "1.0.0")]
public class HelloWorldExample : BaseUnityPlugin
{
    void Awake()
    {
        Debug.Log("Hello World!");
    }
}

