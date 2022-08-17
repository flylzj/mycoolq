# coding: utf-8
import aiohttp


class PcSwitch:
    states_api = "/api/states"
    service_api = "/api/services"
    # 先写死
    pc_list = {
        "pc1": "switch.pc1",
    }
    ON = "on"
    OFF = "off"
    SWITCH = "switch"
    TURN_ON = "turn_on"
    TURN_OFF = "turn_off"

    def __init__(self, host, token):
        self.host = host
        self.token = token
        self.headers = {
            "Authorization": "Bearer {}".format(token),
            'Content-Type': 'application/json'
        }

    async def _get_states_api(self, entity_id):
        states_api = f"{self.host}{self.states_api}/{entity_id}"
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(states_api) as resp:
                return await resp.json()

    async def _post_service_api(self, domain, service, service_data):
        states_api = f"{self.host}{self.service_api}/{domain}/{service}"
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.post(states_api, json=service_data) as resp:
                resp_json = await resp.json()

    async def get_pc_states(self, pc, entity_id):
        states = await self._get_states_api(entity_id)
        message = ""
        if states.get("state") and states.get("state") == self.ON:
            message += f"{pc}状态: 开启"
        else:
            message += f"{pc}状态: 关闭"
        return message

    async def get_all_pc_states(self):
        message = ""
        for pc, entity_id in self.pc_list.items():
            message += await self.get_pc_states(pc, entity_id) + "\n"
        message = message.strip()
        return message

    async def turn_on_off_pc(self, pc, service):
        entity_id = self.pc_list.get(pc)
        if not entity_id:
            return f"电脑{pc}不存在"
        service_data = {
            "entity_id": entity_id
        }
        await self._post_service_api(self.SWITCH, service, service_data)
        return f"{service} success"
