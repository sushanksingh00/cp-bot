import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";


const TagPerformanceGraph = ({tags}) => {
    return (
        <ResponsiveContainer width="100%" height={250}>
            <BarChart data={tags}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="tag_name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="success_rate" fill="#2e7adf" radius={[10, 10, 0, 0]}/>
                {/* <Bar dataKey="weakness_score" fill="#000000"/> */}
            </BarChart>
        </ResponsiveContainer>
    )
}
export default TagPerformanceGraph;