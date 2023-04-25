import './App.css';
import './index.css'
import { useEffect, useState, useRef} from "react";
import DataInputComponent from "./components/DataInputComponent";
import ResultComponent from "./components/ResultComponent";
import {useDispatch, useSelector} from "react-redux";
import {result} from "./redux/actions/resultState.action";
import { YMaps, Map,Placemark} from '@pbe/react-yandex-maps';
import {api_key} from './conf'
import AlertDialog from './components/Dialog';
import CircularIndeterminate from './components/preloader';
import {help_info} from './data_help'

function App() {
    const [dataProducts, dataProductsSet] = useState(null)
    const map = useRef(null);
    const shoppingCart = useSelector(state => state.shoppingCartReducer.shoppingCart)
    const resState = useSelector(state => state.resultStateReducer.resultState)
    const dispatch = useDispatch()
    const [resultProducts, resultProductsSet] = useState(null)
    const [points, pointsSet] = useState([]);
    const ymaps = useRef(null)
    const time_limit = useRef(null);
    const weight_limit = useRef(null);
    const [open, setOpen] = useState(false);
    const [isOpenHelp, setIsOpenHelp] = useState(false);
    const [msg_wrg, setMsg_wrg] = useState("");
    let geoObj = null;
    let multiRoute = null;
    const [isLoad, setIsLoad] = useState(false);
    const [mapCenter, mapCenterSet] =  useState([59.904883, 30.513427]);
    useEffect(()=>{
        if(!dataProducts){
            fetch('/products').then(response=>response.json())
            .then((json) => {
                dataProductsSet(json)
            })
        }
  },[])
    const addObserverClick = (ym) => {
        ymaps.current = ym;

        map.current.events.add('click', (ev)=>{
            const p = ev.get('coords')
            pointsSet(p);
            if(geoObj){
                map.current.geoObjects.remove(geoObj)
            }
            geoObj = new ym.Placemark(p, {}, {
                preset: "islands#circleDotIcon",
                iconColor: '#ff0000'
            });
            map.current.geoObjects.add(geoObj);
        })
        map.current.events.add('boundschange', (ev)=>{
            mapCenterSet(ev.get('newCenter'));
        })
    }
    const RESTRICT_AREA = [
        [59.921955, 30.498686],
        [59.890619, 30.528230],

    ];

    const addRoute = () => {
        console.log(Number(time_limit.current.value), Number(weight_limit.current.value), points, shoppingCart)
        if(Number(time_limit.current.value)> 0 &&  Number(weight_limit.current.value)>0 && points.length>0 && shoppingCart.length>0){
            setIsLoad(true);
            fetch("/route", {
                method: 'POST',
                headers: {
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    "time" : time_limit.current.value,
                    "weight" : weight_limit.current.value,
                    "coordinates": {
                        "longitude" : points[1],
                        "latitude" : points[0]
                    },
                    "list_products" : shoppingCart
                })
            })
            .then((responce)=>{
                if(responce.status != 201){
                    setIsLoad(false)
                    return
                }
                return responce.json()
            }).then((json)=>{
                if(!json){
                    return;
                }
                let route_points = []
                for(let i = 0; i < json.route.length; i++){
                    route_points.push([json.route[i].latitude, json.route[i].longitude])
                }
                multiRoute = new ymaps.current.multiRouter.MultiRoute(
                    {
                        referencePoints: route_points,
                        params: {
                            routingMode: "pedestrian"
                        }
                    },
                    {
                        boundsAutoApply: true
                    }
                );
                resultProductsSet(json);
                setIsLoad(false);
                dispatch(result());
                map.current.geoObjects.add(multiRoute);
            });
        } 
        else{
            if(points.length == 0){
                setMsg_wrg("Пожалуйста, поставьте на карте точку отправления/прибытия.");
            }
            else if(shoppingCart.length == 0){
                setMsg_wrg("Пожалуйста, добавьте в корзину хотя бы один товар.");
            }
            else{
                setMsg_wrg("Введены некорректные значения веса или времени. Пожалуйста, укажите положительные числа.");
            }
            setOpen(true);
        }
    };
    function count_products_initial(){
        let count = 0;
        for(let i = 0; i < shoppingCart.length; i++){
            count += shoppingCart[i].count;
        }
        return count;
    }
    const deleteRoute = ()=>{
        pointsSet([]);
        map.current.geoObjects.removeAll();
    }
    function getCurState(){
        if(resState && resultProducts){
            return <ResultComponent resultData={resultProducts} deleteRoute={deleteRoute} initial_count_product={count_products_initial()}/>
        }
        return <DataInputComponent dataProducts={dataProducts} addRoute={addRoute} time_limit={time_limit} weight_limit={weight_limit}/>
    }
    function get_info(){
        if(resState){
            return "" 
        }
        else{
            return "Для построения маршрута поставьте на карте точку отправления/прибытия"
        }
    }
    function loading(){
        if(isLoad){
            return <CircularIndeterminate/>
        }
    }
    return (
    <div className="App">
        <div>
            {loading()}
            <div className="right">
                {getCurState()}
            </div>
            
            <AlertDialog open={open} setOpen={setOpen} title={"Ошибка"} text={msg_wrg}/>

            <AlertDialog open={isOpenHelp} setOpen={setIsOpenHelp} title={"Справка"} text={help_info}/>
            <div align="center">
                <div className="table">
                    <div className="row">
                        <div align="left" className="cell">
                            <button onClick={()=>setIsOpenHelp(true)}>Справка</button>
                        </div>  
                    </div>
                    <div className="row">
                        <div className="cell">
                            <YMaps  query={{apikey: api_key,
                                ns: "use-load-option",
                                load: "Map,Placemark,control.ZoomControl,control.FullscreenControl,geoObject.addon.balloon",
                            }}>
                                <Map className="map"
                                     modules={["multiRouter.MultiRoute", "control.ZoomControl"]}
                                     state={{ center: mapCenter, zoom: 1 ,
                                        controls: ["zoomControl"]}}
                                     options={{restrictMapArea : RESTRICT_AREA}}
                                     instanceRef={map}
                                     onLoad={addObserverClick}
                                >
                                    <label>{get_info()}</label>
                                </Map>
                            </YMaps>
                           </div>
                    </div>
                </div>
            </div>

        </div>
    </div>
  );
}

export default App;
/*
<div align='center' className='cell'>
                        </div>*/