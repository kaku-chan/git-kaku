import boto3
import json
import os

def lambda_handler(event, context):
    # boto3クライアントを初期化
    client = boto3.client('lambda')
    
    # トリガーイベントログの書き出し
    print(event)
    
    # -----1つ目のLambda関数-----
    # 1つ目のLambda関数の名前と引数
    lambda1_name = 'send-slack-message'
    lambda1_payload = {
        'channel_id': 'C04SG136L66',
        'slack_token': os.environ.get('slack_token'),
        'blocks': [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "請求書がアップロードされました。"
			}
		}
	]
    }

    # 1つ目のLambda関数を呼び出す
    response1 = client.invoke(
        FunctionName=lambda1_name,
        InvocationType='RequestResponse',
        Payload=json.dumps(lambda1_payload)
    )

    # レスポンスを処理する
    response1_payload = json.loads(response1['Payload'].read())
    slack_message_ts = response1_payload.get('message_ts')

    # メッセージIDを表示
    print(f"Slack message ts: {slack_message_ts}")

    # -----2つ目のLambda関数-----
    # 再度send-slack-messageを呼び出すための引数（必要に応じて変更）
    lambda2_payload = {
        'channel_id': 'C04SG136L66',
        'slack_token': os.environ.get('slack_token'),
        'blocks': [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "メタデータを入力して「完了」ボタンを押してください。"
            },
            "accessory": {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "完了",
                    "emoji": True
                },
                "value": "meta-ok",
                "action_id": "button-action"
            }
        }
    ]
    }
    #tset