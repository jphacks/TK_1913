using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class AngleControl : MonoBehaviour
{

  Slider angleSlider;
  GameObject mirai;
  Animator miraiAnimator;
  HumanPose miraiPose;
  HumanPoseHandler handler;
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
  // Use this for initialization
  void Start()
  {

    angleSlider = GetComponent<Slider>();

    float maxValue = 10f;
    float minValue = 0f;
    float startValue = 0f;

    angleSlider.maxValue = maxValue;
    angleSlider.minValue = minValue;
    angleSlider.value = startValue;

  }

  // Update is called once per frame
  void Update()
  {
  }

  public void onValueChanged()
  {
    // ref -> https://squmarigames.com/2018/12/16/unity-beginner-slider/
    Debug.Log("現在値：" + angleSlider.value);
  }

  // Sliderの値を渡す
  public float getAngleSliderNormalizedValue()
  {
    return angleSlider.normalizedValue;
  }

}