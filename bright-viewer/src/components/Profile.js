import React, {Component} from "react";
import Avatar from "react-avatar";
import {RadialChart, Hint, Sankey} from "react-vis";
import "./css/Profile.css";
import '../../node_modules/react-vis/dist/style.css';
import Energy from '../energy.json';

class Profile extends Component{
    state = {
        value: false
    };

    colorScale = [
        "red", "blue", "green"
    ];

    labelStyle = {
        textSize: '2em'
    };

    data = [
        { x: "Republicans", y: 65 },
        { x: "Democrats", y: 10},
        { x: "Libertarians", y: 25}
    ];

    myData = [{name: 'Democrats', angle: 1, color: '#0015bc'}, {name: 'Republicans', angle: 5, color: '#de0100'}, {name: 'Libertarians', angle: 2, color: '#3cd070'}]

    render(){
        const {value} = this.state;
        console.log(this.state.value.name);
        return (
            <div className="profile">
                <div class="left">
                    <Avatar size="200" round={true} src="https://upload.wikimedia.org/wikipedia/commons/e/e1/John_McCain_official_portrait_2009.jpg" />
                    <h1>John  Mccain</h1>
                </div>
                <div class="right">
                <RadialChart colorType='literal' animation 
                    innerRadius={60} radius={90} data={this.myData} 
                    width={200} height={200} showLabels={true} labelsStyle={this.labelStyle}
                    onValueMouseOver={v => this.setState({value: v})}
                    onSeriesMouseOut={v => this.setState({value: false})}
                    padAngle={0.04}>
                    {value !== false &&  <Hint value={[value.name]} />}
                </RadialChart>
                    <h1>Donors</h1>
                </div>
                <Sankey
                    animation
                    margin={50}
                    nodes={Energy.nodes}
                    links={Energy.links}
                    width={960}
                    height={300}
                    layout={24}
                    nodeWidth={15}
                    nodePadding={10}
                    style={{
                    links: {
                        opacity: 0.3
                    },
                    labels: {
                        fontSize: '8px'
                    },
                    rects: {
                        strokeWidth: 2,
                        stroke: '#1A3177'
                    }
                }}
                />
            </div>
       );
    }   
}
export default Profile;