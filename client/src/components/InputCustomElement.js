import * as React from 'react';
export default function InputComponent({label , type, value, onChange, sRef}) {
    return (
        <div>
            <label>
                {label}
            </label>
            <br/>
            <input
                ref={sRef}
                type={type}
                defaultValue={value}
                onChange={onChange}
            />
        </div>
    )
}