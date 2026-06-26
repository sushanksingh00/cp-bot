import React from "react";

import {
    AreaChart,
    Area,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer
} from "recharts";

const ContestRatingChart = ({ contests = [] }) => {

    const contestData = contests.slice().reverse().map(contest => ({
        contest : contest.contest_name,
        rating : contest.new_rating
    }))


    return (
        <div className='p-6 rounded-2xl  p-6 mb-4'>
            <ResponsiveContainer width="100%" height={350}>
                <AreaChart data={contestData}>
                    {/* <CartesianGrid strokeDasharray="3 3" stroke="black"/> */}
                    <YAxis />
                    <Tooltip />
                    <Area type="monotone" dataKey="rating" stroke="black" fill="#2e7adf"></Area>

                </AreaChart>
            </ResponsiveContainer>

        </div>
    );
};

export default ContestRatingChart;