from dishka import Provider, provide, Scope

from app.core.schemas.repo_protocols import AuthRepoProtocol, BankRepoProtocol
from app.core.schemas.service_protocols import (
    RegisterUserServiceProtocol,
    LoginServiceProtocol,
    JWTServiceProtocol,
    CreateBillServiceProtocol,
    GetBillsServiceProtocol,
    GetBillServiceProtocol,
    GetCurrenciesServiceProtocol,
    PaymentServiceProtocol, CachedBillsServiceProtocol,
)
from app.services import (
    RegisterUserService,
    LoginService,
    JWTService,
    CreateBillService,
    GetCurrenciesService,
    GetBillsService,
    GetBillService,
    PaymentService, CachedBillsService,
)


class ServiceProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_register_service(
        self, auth_repo: AuthRepoProtocol
    ) -> RegisterUserServiceProtocol:
        return RegisterUserService(auth_repo)

    @provide(scope=Scope.REQUEST)
    async def get_login_service(
        self, auth_repo: AuthRepoProtocol, jwt_service: JWTServiceProtocol
    ) -> LoginServiceProtocol:
        return LoginService(auth_repo, jwt_service)

    @provide(scope=Scope.REQUEST)
    async def get_jwt_service(
        self,
        auth_repo: AuthRepoProtocol,
    ) -> JWTServiceProtocol:
        return JWTService(auth_repo)

    @provide(scope=Scope.REQUEST)
    async def get_create_bill_service(
        self,
        bill_repo: BankRepoProtocol,
        jwt_service: JWTServiceProtocol,
    ) -> CreateBillServiceProtocol:
        return CreateBillService(bill_repo, jwt_service)

    @provide(scope=Scope.REQUEST)
    async def get_user_bills_service(
        self,
        bill_repo: BankRepoProtocol,
        jwt_service: JWTServiceProtocol,
        cached_service: CachedBillsServiceProtocol,
    ) -> GetBillsServiceProtocol:
        return GetBillsService(bill_repo, jwt_service, cached_service)

    @provide(scope=Scope.REQUEST)
    async def get_bill_service(
        self,
        bill_repo: BankRepoProtocol,
    ) -> GetBillServiceProtocol:
        return GetBillService(bill_repo)

    @provide(scope=Scope.REQUEST)
    async def get_currencies_service(self) -> GetCurrenciesServiceProtocol:
        return GetCurrenciesService()

    @provide(scope=Scope.REQUEST)
    async def get_payment_service(
        self,
        bill_repo: BankRepoProtocol,
    ) -> PaymentServiceProtocol:
        return PaymentService(bill_repo)

    @provide(scope=Scope.REQUEST)
    async def get_caching_service(
        self,
    ) -> CachedBillsServiceProtocol:
        return CachedBillsService()