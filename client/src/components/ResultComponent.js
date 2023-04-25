import {useDispatch} from "react-redux";
import {entry, result} from "../redux/actions/resultState.action";
export default function ResultComponent({resultData, deleteRoute, initial_count_product}){
    const dispatch = useDispatch()
    function get_found_products(count_found_product, initial_count){
        let str = ""
        if (count_found_product % 10 === 1 && count_found_product % 100 !== 11) {
            str += `Найден ${count_found_product} из `
        } else {
            str += `Найдено ${count_found_product} из `
        }
        if (initial_count % 10 === 1 && initial_count % 100 !== 11) {
            str += `${initial_count} товара.`
        } else {
            str += `${initial_count} товаров.`
        }
        return str;
    }
    return (
        <div>
            <div>
                <p>Стоимость корзины: {Math.round(resultData.costs*100)/100} руб.</p>
                <p>Ориентировочное время: {Math.round(resultData.time)} мин.</p>
                <p>{get_found_products(resultData.count, initial_count_product)}</p>
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
        if(resultData.shopping_cart.length){
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
            for(let i = 0; i < resultData.shopping_cart.length; i++){
                content.push(<tr>
                    <td >{i + 1}</td>
                    <td >
                        {resultData.shopping_cart[i].name}
                    </td>
                    <td>
                        {resultData.shopping_cart[i].address}
                    </td>
                    <td>
                        {resultData.shopping_cart[i].count}
                    </td>
                    <td>
                        {resultData.shopping_cart[i].price}
                    </td>
                </tr>)
            }
            table.push(<tbody>{content}</tbody>)
            return <div className="left tableFixHead tableFixHeadResult"><table>{table}</table></div>
        }
        else{
            return <div>Результат не найден. Увеличьте количество времени и/или вес сумки.</div>
        }

    }
}