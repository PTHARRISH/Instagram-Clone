import {
  ArrowLeftOnRectangleIcon,
  ChatBubbleLeftRightIcon,
  Cog6ToothIcon,
  FilmIcon,
  HomeIcon,
  MagnifyingGlassIcon,
  UserIcon,
} from '@heroicons/react/24/outline';
import { useNavigate } from 'react-router-dom';
import { logout } from '../api/auth';

const Sidebar = ({ username, expanded, setExpanded }) => {
  const navigate = useNavigate();

  // Logout handler
  const handleLogout = async () => {
    try {
      const result = await logout(); // Call API + clear tokens
      navigate('/login', { state: { message: result.message } });
    } catch (error) {
      console.error('Logout failed:', error);
      navigate('/login', { state: { message: error.message || 'Logout failed. Please login again.' } });
    }
  };

  // Sidebar menu items
  const menuItems = [
    { icon: HomeIcon, label: 'Home', action: () => navigate('/') },
    { icon: FilmIcon, label: 'Reels', action: () => navigate('/reels') },
    { icon: ChatBubbleLeftRightIcon, label: 'Messages', action: () => navigate('/messages') },
    { icon: MagnifyingGlassIcon, label: 'Explore', action: () => navigate('/explore') },
    { icon: Cog6ToothIcon, label: 'Settings', action: () => navigate('/settings') },
    { icon: UserIcon, label: 'Profile', action: () => navigate(`/profile/${username}`) },
    { icon: ArrowLeftOnRectangleIcon, label: 'Logout', action: handleLogout },
  ];

  return (
    <>
      {/* ===== LAPTOP & TABLET SIDEBAR ===== */}
      <aside
        onMouseEnter={() => setExpanded(true)}
        onMouseLeave={() => setExpanded(false)}
        className={`hidden md:flex fixed left-0 top-0 h-screen
          ${expanded ? 'w-56' : 'w-16'}
          bg-gray-900 border-r border-gray-800
          transition-all duration-300
          flex-col z-50 overflow-hidden`}
      >
        <div className="mt-8 flex flex-col gap-1 px-2">
          {menuItems.map((item, idx) => (
            <button
              key={idx}
              onClick={item.action}
              className="flex items-center gap-4 h-12 px-3 rounded-md
                text-gray-300 hover:text-white hover:bg-gray-800 transition"
            >
              <item.icon className="h-6 w-6 shrink-0" />
              {expanded && (
                <span className="whitespace-nowrap text-sm font-medium">
                  {item.label}
                </span>
              )}
            </button>
          ))}
        </div>
      </aside>

      {/* ===== MOBILE BOTTOM NAV ===== */}
      <nav className="md:hidden fixed bottom-0 left-0 right-0 h-16
        bg-gray-900 border-t border-gray-800 z-50">
        <div className="flex justify-around items-center h-full">
          {menuItems.map((item, idx) => (
            <button
              key={idx}
              onClick={item.action}
              className="flex flex-col items-center text-gray-400 hover:text-white transition"
            >
              <item.icon className="h-6 w-6" />
              <span className="text-xs mt-1">{item.label}</span>
            </button>
          ))}
        </div>
      </nav>
    </>
  );
};

export default Sidebar;
