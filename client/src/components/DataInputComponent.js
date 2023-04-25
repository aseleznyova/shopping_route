import { useRef, useEffect, useState} from "react";
import '../index.css';
import {useDispatch, useSelector} from "react-redux";
import InputComponent from "./InputCustomElement";
import {actionAdd, actionDelete, actionIncrement, actionDicrement} from "../redux/actions/shoppingCart.action";
import {result} from "../redux/actions/resultState.action";
//import * as React from "react";
export default function DataInputComponent({dataProducts, addRoute, time_limit, weight_limit}){
    const [resultSearch, resultSearchState] = useState([])
    const field_result_search = useRef(null)
    const dispatch = useDispatch()
    const shoppingCart = useSelector(state => state.shoppingCartReducer.shoppingCart)
    const valid = (ev)=>{
        console.log(ev.target)
        if(Number(ev.target.value) < 0){
            ev.target.classList.add("wrong")
        }
        else{
            
            ev.target.classList.remove("wrong")
        }}
    return (
        <div>
            <div
                className="left paramsInput"
                onMouseLeave={()=>{
                    field_result_search.current.style.visibility = "hidden"
                }}>
                <InputComponent value={60} type={"number"} sRef={time_limit} label={"Ограничение по времени, мин"} minValue={10} onChange={valid}/>
                <InputComponent value={15} type={"number"} sRef={weight_limit} label={"Максимальный вес сумки, кг"} minValue={1} onChange={valid}/>
                <label>
                    Поиск товара
                </label>
                <br/>
                <input
                    onChange={(event)=>{
                        searchProduct(event.target.value)
                    }}
                    onMouseEnter={()=>{
                        field_result_search.current.style.visibility = "visible"
                    }}
                />
                <div className="customResult" ref={field_result_search}>
                    {getSearch()}
                </div>
            </div>
            <div>
                {getTable()}
            </div>
            <div className="left">
                <button onClick={()=>dispatch(actionDelete(shoppingCart))}>Очистить корзину</button>
                <button onClick={()=>{
                    addRoute()
                }
                }>Построить маршрут</button>
            </div>
        </div>
    )
    function searchProduct(name){
        if(name === "") {
            resultSearchState([])
            return
        }

        let delimeter = /[,. :?!№\"]/;
        let tokens_name = name.split(delimeter).filter(item => item !== "");;
        resultSearchState(dataProducts.filter((item) => {
            let tokens = item.name.split(delimeter).filter(item => item !== "");
            let count = 0;
            for(let k = 0; k < tokens_name.length; k++){
                for(let j =0; j < tokens.length; j++){
                    if(tokens[j].toLowerCase().indexOf(tokens_name[k].toLowerCase()) === 0){
                        count++;
                        break;
                    }
                }
            }
            if(count === tokens_name.length){
                return true;
            }
            return false;
        }));
        //dataProducts.filter(item => item.name.indexOf(name) !==-1));
    }
    function getSearch(){
        let res = []
        for(let i = 0; i < resultSearch.length; i++){
            res.push(
                <div
                    onClick={(event)=>{
                        let index = shoppingCart.findIndex((item)=>{
                            return item.id === resultSearch[i].id
                        })
                        if(index !== -1){
                            dispatch(actionIncrement(shoppingCart[index]))
                        }
                        else {
                            const new_product = {
                                id: resultSearch[i].id,
                                name: resultSearch[i].name,
                                count: 1,
                            }
                            dispatch(actionAdd(new_product))
                        }
                    }}>
                    {resultSearch[i].name}
                </div>
            )
        }
        return res
    }
    function getTable(){
        if (shoppingCart.length === 0){
            return;
        }
        let table = []
        table.push(
                <thead>
                <tr>
                    <th>№</th>
                    <th>Название товара</th>
                    <th>Количество</th>
                </tr>
                </thead>
        );
        let content = []
        for(let i = 0; i < shoppingCart.length; i++){
            content.push(<tr>
                <td >{i + 1}</td>
                <td >
                    {shoppingCart[i].name}
                </td>
                <td>
                    <i onClick={(item)=>{
                        dispatch(actionDicrement(shoppingCart[i]))
                    }} className="fa-solid fa-square-minus fa-xl"></i>

                    {shoppingCart[i].count}
                    <i onClick={()=>{
                        dispatch(actionIncrement(shoppingCart[i]))
                    }} className="fa-solid fa-square-plus fa-xl"></i>
                </td>
            </tr>)}
        table.push(<tbody>{content}</tbody>)
        return <div className="left tableFixHead tableFixHeadInput"><table>{table}</table></div>
    }
}