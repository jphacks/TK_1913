using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System.Runtime.InteropServices;
using UnityEngine.Networking;
using System;  
using System.IO;  
//using System.Net; 
using System.Linq;
using System.Threading.Tasks;

public class Komachi_bow : MonoBehaviour
{
  /*
  [DllImport("__Internal")]
  private static extern string GetBowId();
  */
  
  GameObject mirai, angleSlider;
  Animator miraiAnimator;
  HumanPose miraiPose;
  HumanPoseHandler handler;
  AngleControl angleControlScript;

  public string csvText;
  public List<double[]> csvLines;
  enum Muscles : int
  {
    SpineFrontBack,
    SpineLeftRight,
    SpineTwistLeftRight,
    ChestFrontBack,
    ChestLeftRight,
    ChestTwistLeftRight,
    UpperChestFrontBack,
    UpperChestLeftRight,
    UpperChestTwistLeftRight,
    NeckNodDownUp,
    NeckTiltLeftRight,
    NeckTurnLeftRight,
    HeadNodDownUp,
    HeadTiltLeftRight,
    HeadTurnLeftRight,
    LeftEyeDownUp,
    LeftEyeInOut,
    RightEyeDownUp,
    RightEyeInOut,
    JawClose,
    JawLeftRight,
    LeftUpperLegFrontBack,
    LeftUpperLegInOut,
    LeftUpperLegTwistInOut,
    LeftLowerLegStretch,
    LeftLowerLegTwistInOut,
    LeftFootUpDown,
    LeftFootTwistInOut,
    LeftToesUpDown,
    RightUpperLegFrontBack,
    RightUpperLegInOut,
    RightUpperLegTwistInOut,
    RightLowerLegStretch,
    RightLowerLegTwistInOut,
    RightFootUpDown,
    RightFootTwistInOut,
    RightToesUpDown,
    LeftShoulderDownUp,
    LeftShoulderFrontBack,
    LeftArmDownUp,
    LeftArmFrontBack,
    LeftArmTwistInOut,
    LeftForearmStretch,
    LeftForearmTwistInOut,
    LeftHandDownUp,
    LeftHandInOut,
    RightShoulderDownUp,
    RightShoulderFrontBack,
    RightArmDownUp,
    RightArmFrontBack,
    RightArmTwistInOut,
    RightForearmStretch,
    RightForearmTwistInOut,
    RightHandDownUp,
    RightHandInOut,
    LeftThumb1Stretched,
    LeftThumbSpread,
    LeftThumb2Stretched,
    LeftThumb3Stretched,
    LeftIndex1Stretched,
    LeftIndexSpread,
    LeftIndex2Stretched,
    LeftIndex3Stretched,
    LeftMiddle1Stretched,
    LeftMiddleSpread,
    LeftMiddle2Stretched,
    LeftMiddle3Stretched,
    LeftRing1Stretched,
    LeftRingSpread,
    LeftRing2Stretched,
    LeftRing3Stretched,
    LeftLittle1Stretched,
    LeftLittleSpread,
    LeftLittle2Stretched,
    LeftLittle3Stretched,
    RightThumb1Stretched,
    RightThumbSpread,
    RightThumb2Stretched,
    RightThumb3Stretched,
    RightIndex1Stretched,
    RightIndexSpread,
    RightIndex2Stretched,
    RightIndex3Stretched,
    RightMiddle1Stretched,
    RightMiddleSpread,
    RightMiddle2Stretched,
    RightMiddle3Stretched,
    RightRing1Stretched,
    RightRingSpread,
    RightRing2Stretched,
    RightRing3Stretched,
    RightLittle1Stretched,
    RightLittleSpread,
    RightLittle2Stretched,
    RightLittle3Stretched
  }
  private Animator anim;
  public Slider slider;   //Assign the UI slider of your scene in this slot 
  public double t;
  public double startTime;
  public int lineNum;
  public bool firstTime = true;

  //[SerializeField]
  public string bow_id = "";


  // Use this for initialization

  void GetBowId(string value){
    bow_id = value;
  }
  void Start()
  {
    mirai = GameObject.Find("mirai2019_dance");
    miraiAnimator = mirai.GetComponent<Animator>();
    handler = new HumanPoseHandler(miraiAnimator.avatar, miraiAnimator.transform);
    handler.GetHumanPose(ref miraiPose);
    initZeroPose();
    initUpRightPose();
    //musclesStatus();

    angleSlider = GameObject.Find("Slider");
    angleControlScript = angleSlider.GetComponent<AngleControl>();
    bow_id = "58";
    
  }

  // Update is called once per frame
  
  void Update()
  {
    if (bow_id.Length==0)
    {

    } else if (firstTime)
    {
      string url = "http://komachi.hongo.wide.ad.jp/csv?bow_id=" + bow_id;
      Debug.Log(url);
      
      StartCoroutine(GetText(url));

    } else 
    {
      t += Time.deltaTime;
      getPoseFromCsv(csvLines, startTime);
      handler.SetHumanPose(ref miraiPose);
    }
  }

  private void initZeroPose()
  {
    for (int i = 0; i < HumanTrait.MuscleCount; i++)
    {
      miraiPose.muscles[i] = 0f;
    }
    handler.SetHumanPose(ref miraiPose);
  }

  private void initUpRightPose()
  {
    miraiPose.muscles[(int)Muscles.LeftArmDownUp] = -0.6f;
    miraiPose.muscles[(int)Muscles.LeftArmTwistInOut] = 0.15f;
    miraiPose.muscles[(int)Muscles.LeftForearmStretch] = 1f;
    miraiPose.muscles[(int)Muscles.LeftLowerLegStretch] = 0.88f;
    miraiPose.muscles[(int)Muscles.LeftUpperLegFrontBack] = 0.5f;
    miraiPose.muscles[(int)Muscles.RightArmDownUp] = -0.6f;
    miraiPose.muscles[(int)Muscles.RightArmTwistInOut] = 0.15f;
    miraiPose.muscles[(int)Muscles.RightForearmStretch] = 1f;
    miraiPose.muscles[(int)Muscles.RightLowerLegStretch] = 0.88f;
    miraiPose.muscles[(int)Muscles.RightUpperLegFrontBack] = 0.5f;
    miraiPose.muscles[(int)Muscles.SpineFrontBack] = 0f;
    handler.SetHumanPose(ref miraiPose);
  }

  private void musclesStatus()
  {
    string[] muscleName = HumanTrait.MuscleName;
    int i = 0;
    while (i < HumanTrait.MuscleCount)
    {
      //   switch (i)
      //   {
      //     case (int)Muscles.LeftArmDownUp:
      //     case (int)Muscles.LeftArmTwistInOut:
      //     case (int)Muscles.LeftForearmStretch:
      //     case (int)Muscles.LeftLowerLegStretch:
      //     case (int)Muscles.LeftUpperLegFrontBack:
      //     case (int)Muscles.RightArmDownUp:
      //     case (int)Muscles.RightArmTwistInOut:
      //     case (int)Muscles.RightForearmStretch:
      //     case (int)Muscles.RightLowerLegStretch:
      //     case (int)Muscles.RightUpperLegFrontBack:
      //     case (int)Muscles.SpineFrontBack:
      //       Debug.Log((Muscles)System.Enum.ToObject(typeof(Muscles), i) + ":" + muscleName[i] + ":" + miraiPose.muscles[i]);
      //       break;
      //   }
      Debug.Log((Muscles)System.Enum.ToObject(typeof(Muscles), i) + ":" + muscleName[i] + ":" + miraiPose.muscles[i]);
      i++;
    }
  }

private void getPoseFromCsv(List<double[]> csvLines, double startTime)
  {
    //Debug.Log(t);
    for (int i=lineNum;i<csvLines.Count-1;i++){
      if (csvLines[i][0]-startTime <= t && t < csvLines[i+1][0]-startTime)
      {
        double ratio = (t-csvLines[i][0]+startTime)/(csvLines[i+1][0]-csvLines[i][0]);
        float sliderValue = float.Parse(linearDouble(csvLines[i][1], csvLines[i+1][1], ratio).ToString());
        //Debug.Log(sliderValue);
        // [parameters of bow_3]
        // 21 Left  Upper Leg Front-Back  :  [0.5 ~ -0.5]
        // 29 Right Upper Leg Front-Back  :  [0.5 ~ -0.5]
        // 0  Spine Front-Back            :  [0.0 ~ -0.5]
        // ?  Root Q.x                    :  [0.0 ~ 0.6]
        miraiPose.muscles[(int)Muscles.LeftUpperLegFrontBack] = 0.5f - 1f * sliderValue;
        miraiPose.muscles[(int)Muscles.RightUpperLegFrontBack] = 0.5f - 1f * sliderValue;
        miraiPose.muscles[(int)Muscles.SpineFrontBack] = 0.0f - 0.5f * sliderValue;

        float rot = getRot(sliderValue);
        miraiAnimator.transform.RotateAround(new Vector3(0, 0.8f, 0), new Vector3(1, 0, 0), rot - miraiAnimator.transform.rotation.eulerAngles.x);

        double ovearllRatio = 10*t/(csvLines.Last()[0]-startTime);
        angleControlScript.setSliderValue(float.Parse(ovearllRatio.ToString()));
        return;
      }
    }
    t = 0f;
    initUpRightPose();

  }
  private void getSliderValue()
  {
    float sliderValue = angleControlScript.getAngleSliderNormalizedValue();
    // [parameters of bow_3]
    // 21 Left  Upper Leg Front-Back  :  [0.5 ~ -0.5]
    // 29 Right Upper Leg Front-Back  :  [0.5 ~ -0.5]
    // 0  Spine Front-Back            :  [0.0 ~ -0.5]
    // ?  Root Q.x                    :  [0.0 ~ 0.6]
    miraiPose.muscles[(int)Muscles.LeftUpperLegFrontBack] = 0.5f - 1f * sliderValue;
    miraiPose.muscles[(int)Muscles.RightUpperLegFrontBack] = 0.5f - 1f * sliderValue;
    miraiPose.muscles[(int)Muscles.SpineFrontBack] = 0.0f - 0.5f * sliderValue;

    float rot = getRot(sliderValue);
   // float rot = 130* 0.5f *sliderValue;
    miraiAnimator.transform.RotateAround(new Vector3(0, 0.8f, 0), new Vector3(1, 0, 0), rot - miraiAnimator.transform.rotation.eulerAngles.x);
  }

  private double linearDouble(double min, double max, double ratio)
  {
    return (1-ratio)*min + ratio*max;
  }
  private float linear(float min, float max, float ratio)
  {
    return (1-ratio)*min + ratio*max;
  }
  private float getRot(float ratio)
  {
    float thres1 = 0.5f;
    float tilt1 = 0.5f;
    float max1 = thres1*130*tilt1;

    if (ratio < thres1)
    {
      return linear(0, max1, ratio/thres1);
    }  else if(ratio >= thres1)
    {
      return linear(max1, 130*0.65f, (ratio-thres1)/(1-thres1));
    } else {
      return 130 * 0.65f * ratio;
    }

  }

  IEnumerator GetText(string url)
  {
    using (UnityWebRequest www = UnityWebRequest.Get(url))
    {
      yield return www.SendWebRequest();

      if (www.isNetworkError || www.isHttpError)
      {
          Debug.Log(www.error);
      }
      else
      {
        // Show results as text
        csvText = www.downloadHandler.text;
        Debug.Log(csvText);
        csvLines = ReadCsv(csvText);
        startTime = csvLines[0][0];
        //Debug.Log(startTime);
        lineNum = 0;
        firstTime = false;
      }
    }
  }

  private double str2float(string s)
  {
    return  double.Parse(s, System.Globalization.NumberStyles.Float);
  }
  List<double[]> ReadCsv(string text)
  {
    string[] csvLineString;
    List<double[]> csvLines = new List<double[]>();
    string[] textLines = text.Split('\n');
    for (int i=0;i<textLines.Length;i++)
    {
      if (!string.IsNullOrWhiteSpace(textLines[i])){
        csvLineString = textLines[i].Trim().Split(',');
        double[] csvLine = csvLineString.Select(str2float).ToArray();
        csvLines.Add(csvLine);
      }
    }
    return csvLines;    
  }

}