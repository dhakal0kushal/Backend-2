from django.contrib import admin

from .models.users import User
from .models.transactions import UserTransaction
from .models.withdrawal_address import WithdrawalAddress
from .models.wallets import Wallet


admin.site.register(User)
admin.site.register(UserTransaction)
admin.site.register(WithdrawalAddress)
admin.site.register(Wallet)
