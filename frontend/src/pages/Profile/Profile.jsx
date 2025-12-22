import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import apiClient from '../../api/client';
import Avatar from '../../components/Avatar';
import Button from '../../components/Button';
import Sidebar from '../../components/Sidebar';
import StatItem from '../../components/StatItem';

const Profile = () => {
  const { username } = useParams();
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const res = await apiClient.get(`/profiles/${username}/`);
        setProfile(res.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchProfile();
  }, [username]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-900">
        <div className="h-10 w-10 border-4 border-gray-600 border-t-white rounded-full animate-spin" />
      </div>
    );
  }

  if (!profile) {
    return <p className="text-center mt-10 text-white">Profile not found</p>;
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white overflow-x-hidden">
      <Sidebar
        username={username}
        expanded={sidebarOpen}
        setExpanded={setSidebarOpen}
      />

      <main
        className={`
          transition-all duration-300
          px-4 sm:px-6 lg:px-8
          pt-8
          pb-24 md:pb-8
          ${sidebarOpen ? 'md:ml-56' : 'md:ml-16'}
          flex justify-center
        `}
      >
        <div className="w-full max-w-4xl">

          <div className="flex flex-col md:flex-row gap-10 items-center md:items-start">
            <Avatar src={profile.avatar} size={160} />

            <div className="flex-1 text-center md:text-left">
              <div className="flex flex-col sm:flex-row items-center gap-4 mb-4">
                <h2 className="text-2xl font-semibold">{username}</h2>

                {profile.is_owner && (
                  <Button className="bg-blue-600 hover:bg-blue-700 text-white">
                    Edit Profile
                  </Button>
                )}
              </div>

              <div className="flex justify-center md:justify-start gap-10 mb-4">
                <StatItem value="0" label="Posts" />
                <StatItem value={profile.followers_count} label="Followers" />
                <StatItem value={profile.following_count} label="Following" />
              </div>

              <p className="font-medium">{username}</p>
              {profile.bio && (
                <p className="text-gray-400">{profile.bio}</p>
              )}
            </div>
          </div>

          <div className="border-t border-gray-700 mt-10 pt-6 text-center text-gray-400">
            No posts yet
          </div>
        </div>
      </main>
    </div>
  );
};

export default Profile;
