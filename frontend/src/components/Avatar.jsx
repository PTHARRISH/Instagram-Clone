import defaultAvatar from '../assets/images/user.png';

const Avatar = ({ src, size = 120 }) => {
  return (
    <img
      src={src || defaultAvatar}
      alt="avatar"
      className="rounded-full object-cover border-4 border-black"
      style={{ width: size, height: size }}
    />
  );
};

export default Avatar;
