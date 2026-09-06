import asyncio
from contextlib import asynccontextmanager, suppress

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import dispatch, health, live, recommendations, routes, scenarios, vehicles
from app.config import get_settings
from app.services.live_updates import live_updates
from app.services.state_store import StateStore


async def simulation_loop(app: FastAPI) -> None:
    while True:
        await asyncio.sleep(1)
        store: StateStore = app.state.store
        store.refresh_simulations()
        for dispatch_item in store.dispatches.values():
            vehicle = store.vehicles.get(dispatch_item.vehicle_id)
            if vehicle:
                await live_updates.publish(
                    "vehicle.updated",
                    vehicle.model_dump(mode="json", by_alias=True),
                )


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.store = StateStore(get_settings())
    task = asyncio.create_task(simulation_loop(app))
    yield
    task.cancel()
    with suppress(asyncio.CancelledError):
        await task


app = FastAPI(
    title="UrbanFlow API",
    version="0.1.0",
    description="API wspomagania dyspozytora komunikacji miejskiej.",
    lifespan=lifespan,
)

settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_prefix = "/api/v1"
app.include_router(health.router, prefix=api_prefix)
app.include_router(vehicles.router, prefix=api_prefix)
app.include_router(routes.router, prefix=api_prefix)
app.include_router(recommendations.router, prefix=api_prefix)
app.include_router(dispatch.router, prefix=api_prefix)
app.include_router(scenarios.router, prefix=api_prefix)
app.include_router(live.router, prefix=api_prefix)
