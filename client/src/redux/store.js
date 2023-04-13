import {applyMiddleware, combineReducers, legacy_createStore as createStore} from "redux";
import {shoppingCartReducer} from "./reducers/shoppingCart.reducer";
import {resultStateReducer} from "./reducers/resultState.reducer";
import {composeWithDevTools} from "redux-devtools-extension";
import thunk from "redux-thunk";

const rootReducer = combineReducers({
    shoppingCartReducer: shoppingCartReducer,
    resultStateReducer: resultStateReducer,
})

export const store = createStore(rootReducer, composeWithDevTools(applyMiddleware(thunk)))