import CalendarHeatmap from "react-calendar-heatmap";
import "react-calendar-heatmap/dist/styles.css";
import DailyActivity from "../pages/daily_activity";
import './DailyActivityHeapMap.css'
import { Link } from "react-router-dom";

const DailyActivityHeatMap = ({ activity }) => {

    const endDate = new Date();

    const startDate = new Date();
    startDate.setMonth(startDate.getMonth() - 4);

    return (
        <div className="bg-gray-200 rounded-2xl shadow-lg p-6">
            <div className="w-full">
                <CalendarHeatmap
                    startDate={startDate}
                    endDate={endDate}
                    values={activity}
                    classForValue={(value) => {
                        if (!value) return "color-empty";
                        if (value.solved_count >= 4) return "color-github-4";
                        if (value.solved_count >= 3) return "color-github-3";
                        if (value.solved_count >= 2) return "color-github-2";
                        return "color-github-1";
                    }}
                />
            </div>
        </div>
    );
};

export default DailyActivityHeatMap;