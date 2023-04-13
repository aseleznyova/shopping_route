import {defaultState} from "../defaultState";
import {
    RESULT_RECIVED,
    DATA_ENTRY
} from "../constants";
export const resultStateReducer = (state = defaultState, action) => {
    switch (action.type){
        case RESULT_RECIVED:
            return {...state, resultState: true}
        case DATA_ENTRY:
            return {...state, resultState: false}
        default:
            return state
    }
}