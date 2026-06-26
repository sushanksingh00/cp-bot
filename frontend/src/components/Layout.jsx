import Sidebar from "./Sidebar";

const Layout = ({children}) => {

    return(
        <div className="flex">
            <Sidebar />
            <div className="flex-1 ml-20 p-4 md:p-6 bg-gray-100 min-h-screen">
                {children}
            </div>
        </div>
    )
}
export default Layout;