
class Response(object):
    '''Response

    arguments:
        success - Boolean
        result - str
        error - str
        execution_time - datetime
    '''
    def __init__(self,
            success=True,
            result='',
            error='',
            execution_time=''
        ):
        self.success = success
        self.result = result
        self.error = error
        self.execution_time = execution_time

    def __str__(self):
        msg = '''
            success: {s}
            result: {r}
            error: {e}
            execution_time: {ex}
        '''.format(
            s=self.success,
            r=self.result,
            e=self.error,
            ex=self.execution_time

        )
        return msg