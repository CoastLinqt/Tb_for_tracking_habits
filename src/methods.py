



async def authenticate_user(
    api_key: str = Header(None),
    session: AsyncSession = Depends(get_async_session),
):

    user_auth = await session.execute(select(Users).where(Users.api_key == api_key))

    if user_auth.scalar() is None:
        new_user = Users(name=fake_name.name(), api_key=api_key)
        session.add(new_user)
        await session.commit()

        user_new = await get_user_by_api_key(api_key=new_user.api_key, session=session)  # type: ignore

        return user_new

    user = await get_user_by_api_key(api_key=api_key, session=session)

    return user