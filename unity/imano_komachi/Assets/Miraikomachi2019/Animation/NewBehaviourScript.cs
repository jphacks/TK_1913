using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class NewBehaviourScript : MonoBehaviour
{
  public Komachi_bow komachi_bow;
  public Text txt;
  private float getValue;

  // Use this for initialization
  void Start()
  {
  }

  // Update is called once per frame
  void Update()
  {
    getValue = komachi_bow.valueFromMqtt;
    txt.text = (getValue * 90).ToString();
  }
}