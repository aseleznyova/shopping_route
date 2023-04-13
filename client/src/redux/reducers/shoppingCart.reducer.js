import {defaultState} from "../defaultState";
import {ADD_PRODUCT,
    DELETE_PRODUCTS,
    DICREMENT_COUNT_PRODUCT,
    INCREMENT_COUNT_PRODUCT} from "../constants";

export const shoppingCartReducer = (state = defaultState, action) => {
    switch (action.type){
        case ADD_PRODUCT:
            if(!state.shoppingCart.find( function(item){
                return item.id === action.payload.id
            })){
                return {...state, shoppingCart: [...state.shoppingCart, action.payload]}
            }
            return {...state, shoppingCart: state.shoppingCart}
        case DELETE_PRODUCTS:
            return {...state, shoppingCart: []}
        case DICREMENT_COUNT_PRODUCT:
            let products = Array.from(state.shoppingCart)
            for(let i = 0; i < products.length; i++){
                if(products[i].id === action.payload.id){
                    if(products[i].count > 1){
                        products[i].count -=1
                    }
                    else if(products[i].count === 1){
                        products = products.filter(item => item.id !== action.payload.id)
                    }
                    break;
                }
            }
            return {...state, shoppingCart: products}
        case INCREMENT_COUNT_PRODUCT:
            let inc_products = Array.from(state.shoppingCart)
            for(let i = 0; i < inc_products.length; i++){
                if(inc_products[i].id === action.payload.id){
                    inc_products[i].count +=1
                    break;
                }
            }
            return {...state, shoppingCart: inc_products}
        default:
            return state
    }
}