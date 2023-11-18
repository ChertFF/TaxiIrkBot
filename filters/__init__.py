from .private_chat import IsPrivate
from .our_chats_id import IsOurChats
from .in_city_list import InCityList
from .in_time_list import InTimeList
from .in_morning_time_list import InMorningTimeList
from loader import dp

dp.filters_factory.bind(IsOurChats)
dp.filters_factory.bind(IsPrivate)
dp.filters_factory.bind(InCityList)
dp.filters_factory.bind(InTimeList)
dp.filters_factory.bind(InMorningTimeList)
