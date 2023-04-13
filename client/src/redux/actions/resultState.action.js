import {RESULT_RECIVED, DATA_ENTRY} from "../constants";

export function entry(){
    return {
        type: DATA_ENTRY
    }
}
export function result(){
    return {
        type: RESULT_RECIVED
    }
}