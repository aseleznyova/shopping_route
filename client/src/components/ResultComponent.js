import {useDispatch} from "react-redux";
import {entry, result} from "../redux/actions/resultState.action";
export default function ResultComponent({resultData, deleteRoute}){
    const dispatch = useDispatch()
    return (
        <div>
            <div>
                <p>Стоимость корзины: {resultData.sumPrice} руб.</p>
                <p>Ориентировочное время: {resultData.time} мин.</p>
            </div>
            <div>
                {getTable()}
            </div>
            <div className="left">
                <button onClick={()=>{
                    dispatch(entry())
                    deleteRoute()
                }}>Сбросить</button>
            </div>
        </div>
    )

    function getTable(){
        if(resultData.cart.length){
            let table = []
            table.push(
                <thead>
                    <tr>
                        <th></th>
                        <th>Название товара</th>
                        <th>Где купить</th>
                        <th>Кол-во</th>
                        <th>Стоимость за шт</th>
                    </tr>
                    </thead>
            );
            let content = []
            for(let i = 0; i < resultData.cart.length; i++){
                content.push(<tr>
                    <td >{i + 1}</td>
                    <td >
                        {resultData.cart[i].name}
                    </td>
                    <td>
                        {resultData.cart[i].address}
                    </td>
                    <td>
                        {resultData.cart[i].count}
                    </td>
                    <td>
                        {resultData.cart[i].price}
                    </td>
                </tr>)
            }
            table.push(<tbody>{content}</tbody>)
            return <div className="left tableFixHead"><table>{table}</table></div>
        }
        else{
            return <div>Результат не найден</div>
        }

    }
}