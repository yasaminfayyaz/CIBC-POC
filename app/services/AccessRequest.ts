import {BASE_URL} from '../constants/BaseUrl';
import {APIResponse} from '../types/APIResponse';
import {AccessRequest} from '../types/AccessRequestTypes';

/**
 *
 * @param contextualInfo Contextual information gathered by the device
 * @param token Authorization token containing employee ID, etc.
 * @returns Returns an API Response object informing if access request was authorized or not, or an error message.
 */
export const postAccessRequest = async (
  contextualInfo: AccessRequest,
  token?: string,
): Promise<APIResponse> => {
  const response = await fetch(`${BASE_URL}/`, {
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    method: 'POST',
    body: JSON.stringify({...contextualInfo}),
  });

  const responseBody = await response.json();

  return responseBody;
};
