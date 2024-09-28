import requests

                    
class Notification: 

    def send_lotto_buying_message(self, body: dict, token: str, channel: str) -> None:
        assert type(token) == str
        assert type(channel) == str
      
        result = body.get("result", {})
        if result.get("resultMsg", "FAILURE").upper() != "SUCCESS":  
            return

        lotto_number_str = self.make_lotto_number_message(result["arrGameChoiceNum"])
        message = f"{result['buyRound']}회 로또 구매 완료 :moneybag: 남은잔액 : {body['balance']}\n```{lotto_number_str}```"
        self._send_slack_webhook(token, channel, message)

    def make_lotto_number_message(self, lotto_number: list) -> str:
        assert type(lotto_number) == list

        # parse list without last number 3
        lotto_number = [x[:-1] for x in lotto_number]
        
        # remove alphabet and | replace white space  from lotto_number
        lotto_number = [x.replace("|", " ") for x in lotto_number]
        
        # lotto_number to string 
        lotto_number = '\n'.join(x for x in lotto_number)
        
        return lotto_number

    def send_win720_buying_message(self, body: dict, token: str, channel: str) -> None:
        assert type(token) == str
        assert type(channel) == str
        
        if body.get("resultCode") != '100':  
            return       

        win720_round = body.get("resultMsg").split("|")[3]

        win720_number_str = self.make_win720_number_message(body.get("saleTicket"))
        message = f"{win720_round}회 연금복권 구매 완료 :moneybag: 남은잔액 : {body['balance']}\n```{win720_number_str}```"

    def make_win720_number_message(self, win720_number: str) -> str:
        return "\n".join(win720_number.split(","))

    def send_lotto_winning_message(self, winning: dict, token: str, channel: str) -> None: 
        assert type(winning) == dict
        assert type(token) == str
        assert type(channel) == str

        try: 
            round = winning["round"]
            money = winning["money"]
            message = f"로또 *{winning['round']}회* - *{winning['money']}* 당첨 되었습니다 :tada:"
            self._send_slack_webhook(token, channel, message)
        except KeyError:
            return

    def send_win720_winning_message(self, winning: dict, token: str, channel: str) -> None: 
        assert type(winning) == dict
        assert type(token) == str
        assert type(channel) == str

        try: 
            round = winning["round"]
            money = winning["money"]
            message = f"연금복권 *{winning['round']}회* - *{winning['money']}* 당첨 되었습니다 :tada:"
            self._send_slack_webhook(token, channel, message)
        except KeyError:
            return

    def _send_slack_webhook(self, token: str, channel: str, message: str) -> None:        
        payload = { "channel": channel }
        headers = { "Content-Type": "application/json", "Authorization": f"Bearer {token}" }
        requests.post("https://slack.com/api/chat.postMessage", json=payload, headers=headers)
