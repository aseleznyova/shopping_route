import {ADD_PRODUCT,
    DELETE_PRODUCTS,
    DICREMENT_COUNT_PRODUCT,
    INCREMENT_COUNT_PRODUCT} from "../constants";
export function actionAdd(payload){
    return {
        type: ADD_PRODUCT,
        payload: payload
    }
}

export function actionDelete(payload){
    return {
        type: DELETE_PRODUCTS,
        payload: payload
    }
}

export function actionIncrement(payload){
    return {
        type: INCREMENT_COUNT_PRODUCT,
        payload: payload
    }
}
export function actionDicrement(payload){
    return {
        type: DICREMENT_COUNT_PRODUCT,
        payload: payload
    }
}