function data = vota_read( fname,mname )
%VOTA_READ Summary of this function goes here
%   Detailed explanation goes here
data=h5read(fname,strcat('/measurement/',mname,'/buffer'));

end

