using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MoveObject : MonoBehaviour
{
    float fowardMax =200.0f; //�·� �̵������� (x)�ִ밪

    float backMax = -2.0f; //��� �̵������� (x)�ִ밪

    float currentPosition; //���� ��ġ(x) ����

    float direction = -6.0f; //�̵��ӵ�+����




    void Start()

    {

        currentPosition = transform.position.x + 30;

    }
    void Update()

    {

        currentPosition += Time.deltaTime * direction;


        //���� ��ġ(x)�� �·� �̵������� (x)�ִ밪���� ũ�ų� ���ٸ�

        //�̵��ӵ�+���⿡ -1�� ���� ������ ���ְ� ������ġ�� �·� �̵������� (x)�ִ밪���� ����

       // transform.position = new Vector3(-62.7f, 4.3f, currentPosition);
        transform.position = new Vector3(currentPosition, 3.0f, 38.76f);

        //"Stone"�� ��ġ�� ���� ������ġ�� ó��

    }
}
