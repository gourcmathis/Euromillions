from domain import myModel as mod
from fastapi.routing import APIRouter
import pickle
from sklearn.metrics import classification_report, confusion_matrix

TAG="model"
router = APIRouter(tags=[TAG])



@router.get("/api/model")
async def infos_model():
    """gives information about the model

    Returns:
        Dict[str,Any]: name, confusion matrix and classification report 
    """
    model = pickle.load(open("save.p","rb"))
    X_test = model[1][1]
    y_test = model[1][3]
    y_pred = model[0].predict(X_test)
    return {
        "nom" : "Eurosimulateur",
        "Matrice de confusion":confusion_matrix(y_test, y_pred).tolist(),
        "Récapitulatif (avec classe 0 : Tirage perdant / classe 1 : tirage gagnant)":classification_report(y_test, y_pred, output_dict=True)
        } 

@router.put("/api/model")
async def ajout_elem(tirage: mod.Tirage):
    """Add a data to the model

    Args:
        tirage (mod.Tirage): a euromilion type draw

    Returns:
        Dict[str, mod.Tirage]: draw added to the model 
    """
    mod.inputData.append({"N1":tirage.N1,"N2":tirage.N2,"N3":tirage.N3,"N4":tirage.N4,"N5":tirage.N5,"E1":tirage.E1,"E2":tirage.E2}, ignore_index=True)
    return {"La donnée suivante a été ajoutée au model": tirage}

@router.post("/api/model/retrain")
async def retrain_model():
    """retrain the model and save it

    Returns:
        str: print a confirmation message
    """
    model = mod.trainModel(mod.inputData)
    pickle.dump(model,open("save.p","wb"))
    return {"Model réentrainé"} 