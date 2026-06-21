import CalendarHeatmap from "react-calendar-heatmap";
import "react-calendar-heatmap/dist/styles.css";
import DailyActivity from "../pages/daily_activity";
import './DailyActivityHeapMap.css'

const DailyActivityHeatMap = ({ activity }) => {

    return (
        <div className="bg-gray-200 rounded-2xl shadow-lg p-6 hover:shadow-xl transition">
            <CalendarHeatmap
                startDate={new Date("2026-01-01")}
                endDate={new Date()}
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
    );
};

export default DailyActivityHeatMap;