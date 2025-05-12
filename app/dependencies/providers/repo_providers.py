from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.schemas.repo_protocols import AuthRepoProtocol, BankRepoProtocol
from app.repositories import AuthRepo, BankRepo


class RepoProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_auth_repo(self, con: AsyncSession) -> AuthRepoProtocol:
        return AuthRepo(con)

    @provide(scope=Scope.REQUEST)
    async def get_bank_repo(self, con: AsyncSession) -> BankRepoProtocol:
        return BankRepo(con)
