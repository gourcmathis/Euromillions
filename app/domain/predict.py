from domain import myModel as mod
from fastapi.routing import APIRouter
import pickle
import pandas as pd

TAG="predict"
router = APIRouter(tags=[TAG])



@router.post("/api/predict")
async def create_predict(tirage: mod.Tirage):
    """Informs about the chances of winning or not of a draw

    Args:
        tirage (mod.Tirage): arg value

    Returns:
        Dict[str,float]: The return value
    """
    model = pickle.load(open("save.p","rb"))
    res = model[0].predict_proba(pd.DataFrame([{"N1":tirage.N1,"N2":tirage.N2,"N3":tirage.N3,"N4":tirage.N4,"N5":tirage.N5,"E1":tirage.E1,"E2":tirage.E2}]))
    return {
        "proba de gagner" : float(res[0][1]),
        "proba de perdre" : 1-(float(res[0][1]))
        } 


@router.get("/api/predict")
async def create_tirage():
    """created a draw that has a (small) chance of winning

    Returns:
        Dict[str,Dict[str,Any]]: The return value
    """
    return {"Tirage (presque) gagnant" : mod.generateGrid()}

